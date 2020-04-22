import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { HashRouter as Router, Switch, Route } from 'react-router-dom';
import { Demo } from './components';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      backgroundColor: theme.palette.primary.light,
      height: '100vh',
    },
  })
);

export const App: React.FC = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Router>
         <Switch>
          <Route exact path="/demo" component={() => <Demo/>} />
        </Switch>
      </Router>
    </div>
  );
};
