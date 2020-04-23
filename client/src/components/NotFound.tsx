import React from 'react';
import { Container, Typography } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      width: '100%',
      padding: theme.spacing(5),
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: theme.palette.background.default,
      color: theme.palette.primary.main,
    },
  })
);

export const NotFound: React.FC = () => {
  const classes = useStyles();

  return (
    <Container className={classes.root}>
      <Typography variant="h3">
        404, we couldn't find the page you are looking for.
      </Typography>
    </Container>
  );
};