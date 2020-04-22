import React, { useState } from 'react';
import { Button, Container, FormLabel } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import placeholder from '../../assets/placeholder.jpg';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    },
    inputImage: {
      display: 'none'
    },
    image: {
      width: 'min(90%, 500px)',
      margin: theme.spacing(2),
      borderRadius: theme.spacing(1)
    },
    buttonBar: {
      display: 'flex',
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'space-around',
      width: 'min(90%, 500px)'
    },
    imageButton: {
      width: 150,
      padding: theme.spacing(1),
    },
    predictButton: {
      width: 150,
      color: theme.palette.primary.main,
      borderColor: theme.palette.primary.main,
    }
  })
);

export const ImagePicker: React.FC = () => {
  const [imageUploadedStatus, setImageUploadedStatus] = useState<boolean>(false);
  const [imageBase64, setImageBase64] = useState<string | ArrayBuffer | null>(placeholder);
  const classes = useStyles();

  const handleOnImageInputChange = (files: FileList | null): void => {
    if (!files) return;
    const imageFile: File = files[0];
    const fileReader = new FileReader();
    fileReader.readAsDataURL(imageFile);
    fileReader.onload = (event: Event) => setImageBase64(fileReader.result);
    if (!imageUploadedStatus) setImageUploadedStatus(true);
  };

  return (
    <Container className={classes.root}>
      <input
        accept="image/*"
        className={classes.inputImage}
        id="image"
        type="file"
        onChange={({ target: { files } }) => handleOnImageInputChange(files)}
      />
      <img src={typeof imageBase64 === 'string' ? imageBase64 : placeholder} className={classes.image} alt="retina"/>
      <Container className={classes.buttonBar}>
        <FormLabel htmlFor="image">
          <Button className={classes.imageButton} component="span">
            { imageUploadedStatus ? 'Change Image' : 'Upload Image' }
          </Button>
        </FormLabel>
        <Button className={classes.predictButton} component="span" disabled={!imageUploadedStatus} variant="outlined">
          Predict
        </Button>
      </Container>
    </Container>
  );
};