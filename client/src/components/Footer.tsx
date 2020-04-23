import React from 'react';
import { Box, Typography } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      width: '100%',
      backgroundColor: theme.palette.primary.dark,
      padding: theme.spacing(2),
      color: '#fff',
      textAlign: 'center',
      position: 'fixed',
      bottom: 0
    }
  })
);

export const Footer: React.FC = () => {
  const classes = useStyles();
  const HeartEmoji: React.FC = () => <span aria-label="heart" role="img">❤️</span>;

  return (
    <Box className={classes.root}>
      <Typography variant="subtitle1">
        Made with <HeartEmoji/> in Hong Kong, 2020. 
      </Typography>
    </Box>
  );
};