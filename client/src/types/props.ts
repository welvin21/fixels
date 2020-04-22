import { Result } from './result';

export interface ImagePickerProps {
  imageBase64: string | ArrayBuffer | null;
  setImageBase64: (inputImage: string | ArrayBuffer | null) => void;
  setResult: (result: Result) => void;
}

export interface ResultScreenProps {
  result: Result | null;
}
