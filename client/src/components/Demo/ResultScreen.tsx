import React from 'react';
import { ResultScreenProps } from '../../types';

export const ResultScreen: React.FC<ResultScreenProps> = ({ result }) => {
  if(!result)
    return <div>An error has occured.</div>
  else
    return (
      <div>{JSON.stringify(result)}</div>
    );
}