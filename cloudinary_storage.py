"""
Cloudinary Storage Integration for comfyui-vrgamedevgirl
Upload videos and audio to Cloudinary for RunningHub compatibility

Usage:
    storage = CloudinaryStorage(cloud_name, api_key, api_secret)
    result = storage.upload_video(file_path, folder)
"""

import os
import hashlib
from typing import Optional, Dict, Any

# Lazy import cloudinary to avoid errors if not installed
cloudinary = None
cloudinary_uploader = None
cloudinary_api = None


def init_cloudinary(cloud_name, api_key, api_secret):
    """Initialize Cloudinary SDK with configuration"""
    global cloudinary, cloudinary_uploader, cloudinary_api

    if cloudinary is not None:
        return True

    try:
        import cloudinary
        import cloudinary.uploader as cloudinary_uploader
        import cloudinary.api as cloudinary_api

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        return True
    except ImportError:
        print("[Cloudinary] Error: cloudinary package not installed. Run: pip install cloudinary")
        return False
    except Exception as e:
        print(f"[Cloudinary] Initialization error: {e}")
        return False


def generate_unique_filename(base_name: str, extension: str) -> str:
    """Generate a unique filename with hash to avoid collisions"""
    import time
    timestamp = str(int(time.time() * 1000))
    unique_id = hashlib.md5(f"{base_name}{timestamp}".encode()).hexdigest()[:8]
    return f"{base_name}_{unique_id}.{extension}"


class CloudinaryStorage:
    """
    Cloudinary storage handler for video and audio files.
    Supports upload, retrieval, and deletion of media assets.
    """

    def __init__(self, cloud_name: str, api_key: str, api_secret: str, enabled: bool = True):
        self.enabled = enabled
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        self._initialized = False
        self.upload_results_cache = {}

    def _ensure_initialized(self) -> bool:
        if not self.enabled:
            return False
        if not self._initialized:
            self._initialized = init_cloudinary(self.cloud_name, self.api_key, self.api_secret)
        return self._initialized

    def upload_file(
        self,
        file_path: str,
        resource_type: str = "video",
        folder: str = "vrgamedevgirl",
        public_id: Optional[str] = None,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to Cloudinary.

        Args:
            file_path: Local path to the file
            resource_type: "video", "image", or "raw"
            folder: Cloudinary folder to store the file
            public_id: Custom public_id (without extension), auto-generated if None
            tags: Optional list of tags for the asset

        Returns:
            Dict with upload result including:
            - success: bool
            - url: str (secure URL)
            - public_id: str
            - asset_id: str
            - error: str (if failed)
        """
        if not self._ensure_initialized():
            return {"success": False, "error": "Cloudinary not initialized"}

        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            # Generate public_id if not provided
            if public_id is None:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                ext = os.path.splitext(file_path)[1].lower().lstrip(".")
                public_id = generate_unique_filename(base_name, "")

            # Default tags
            if tags is None:
                tags = ["vrgamedevgirl", "comfyui"]

            # Upload parameters
            upload_params = {
                "resource_type": resource_type,
                "folder": folder,
                "public_id": public_id,
                "tags": tags,
                "overwrite": False
            }

            print(f"[Cloudinary] Uploading {file_path} to {folder}/{public_id}")

            result = cloudinary_uploader.upload(file_path, **upload_params)

            # Cache result for quick access
            self.upload_results_cache[public_id] = result

            return {
                "success": True,
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "asset_id": result.get("asset_id"),
                "resource_type": result.get("resource_type"),
                "format": result.get("format"),
                "bytes": result.get("bytes"),
                "duration": result.get("duration"),
                "width": result.get("width"),
                "height": result.get("height"),
                "raw_response": result
            }

        except Exception as e:
            error_msg = f"[Cloudinary] Upload failed: {e}"
            print(error_msg)
            return {"success": False, "error": str(e)}

    def upload_video(
        self,
        file_path: str,
        folder: str = "vrgamedevgirl/videos",
        public_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a video file to Cloudinary"""
        return self.upload_file(
            file_path=file_path,
            resource_type="video",
            folder=folder,
            public_id=public_id,
            tags=["vrgamedevgirl", "video", "comfyui"]
        )

    def upload_audio(
        self,
        file_path: str,
        folder: str = "vrgamedevgirl/audio",
        public_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload an audio file to Cloudinary"""
        return self.upload_file(
            file_path=file_path,
            resource_type="video",  # Cloudinary processes audio as video resource
            folder=folder,
            public_id=public_id,
            tags=["vrgamedevgirl", "audio", "comfyui"]
        )

    def get_url(self, public_id: str, resource_type: str = "video") -> Optional[str]:
        """Get the secure URL for an uploaded asset"""
        if not self._ensure_initialized():
            return None

        # Check cache first
        if public_id in self.upload_results_cache:
            return self.upload_results_cache[public_id].get("secure_url")

        try:
            result = cloudinary_api.resource(f"{resource_type}/{public_id}")
            return result.get("secure_url")
        except Exception as e:
            print(f"[Cloudinary] Failed to get URL for {public_id}: {e}")
            return None

    def delete_asset(self, public_id: str, resource_type: str = "video") -> bool:
        """Delete an asset from Cloudinary"""
        if not self._ensure_initialized():
            return False

        try:
            result = cloudinary_uploader.destroy(f"{resource_type}/{public_id}")
            if result.get("result") == "ok":
                self.upload_results_cache.pop(public_id, None)
                print(f"[Cloudinary] Deleted {public_id}")
                return True
            else:
                print(f"[Cloudinary] Delete failed for {public_id}: {result}")
                return False
        except Exception as e:
            print(f"[Cloudinary] Delete error: {e}")
            return False

    def list_assets(
        self,
        folder: str = "vrgamedevgirl",
        resource_type: str = "video",
        max_results: int = 100
    ) -> list:
        """List assets in a Cloudinary folder"""
        if not self._ensure_initialized():
            return []

        try:
            result = cloudinary_api.resources(
                type="upload",
                prefix=f"{folder}/",
                resource_type=resource_type,
                max_results=max_results
            )
            return result.get("resources", [])
        except Exception as e:
            print(f"[Cloudinary] List error: {e}")
            return []


# Global instance for easy access
_storage_instance = None


def get_storage(enabled: bool = True) -> CloudinaryStorage:
    """Get or create the global CloudinaryStorage instance"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = CloudinaryStorage(enabled=enabled)
    return _storage_instance


# Convenience functions for direct use

def upload_video_to_cloudinary(
    file_path: str,
    folder: str = "vrgamedevgirl/videos",
    cloud_name: str = "dftco0cki",
    api_key: str = "192422146789215",
    api_secret: str = "HKcrrpmDGP2u0qimbuweYxfnlt4"
) -> Dict[str, Any]:
    """Quick function to upload a video to Cloudinary"""
    storage = CloudinaryStorage(cloud_name, api_key, api_secret, enabled=True)
    return storage.upload_video(file_path, folder)


def upload_audio_to_cloudinary(
    file_path: str,
    folder: str = "vrgamedevgirl/audio",
    cloud_name: str = "dftco0cki",
    api_key: str = "192422146789215",
    api_secret: str = "HKcrrpmDGP2u0qimbuweYxfnlt4"
) -> Dict[str, Any]:
    """Quick function to upload an audio to Cloudinary"""
    storage = CloudinaryStorage(cloud_name, api_key, api_secret, enabled=True)
    return storage.upload_audio(file_path, folder)
