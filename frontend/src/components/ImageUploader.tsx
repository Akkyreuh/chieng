import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon } from 'lucide-react';
import { UploadedImage } from '../types';

interface ImageUploaderProps {
  onImageUpload: (image: UploadedImage) => void;
  isLoading: boolean;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageUpload, isLoading }) => {
  const [uploadedImage, setUploadedImage] = useState<UploadedImage | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const preview = URL.createObjectURL(file);
      
      const image: UploadedImage = {
        file,
        preview
      };
      
      setUploadedImage(image);
      onImageUpload(image);
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: isLoading
  });

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleNewUpload = () => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage.preview);
    }
    setUploadedImage(null);
  };

  return (
    <div className="upload-section">
      {!uploadedImage ? (
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          <div className="dropzone-content">
            <Upload size={48} className="upload-icon" />
            <h3>
              {isDragActive ? 'Déposez votre image ici' : 'Glissez-déposez une image de chien'}
            </h3>
            <p>ou cliquez pour sélectionner un fichier</p>
            <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.7 }}>
              Formats supportés: JPEG, PNG, WebP (max. 10MB)
            </p>
          </div>
        </div>
      ) : (
        <div className="image-preview">
          <img 
            src={uploadedImage.preview} 
            alt="Image uploadée" 
            className="preview-image"
          />
          <div className="image-info">
            <p><strong>Fichier:</strong> {uploadedImage.file.name}</p>
            <p><strong>Taille:</strong> {formatFileSize(uploadedImage.file.size)}</p>
            <p><strong>Type:</strong> {uploadedImage.file.type}</p>
          </div>
          {!isLoading && (
            <button 
              onClick={handleNewUpload}
              className="btn"
              style={{ marginTop: '15px' }}
            >
              <ImageIcon size={16} />
              Changer d'image
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
