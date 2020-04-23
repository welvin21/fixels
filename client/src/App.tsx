import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { HashRouter as Router, Switch, Route } from 'react-router-dom';
import { Demo, Header, NotFound } from './components';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      backgroundColor: theme.palette.background.default,
    },
  })
);

export const App: React.FC = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Router>
        <Header/>
        <Switch>
          <Route exact path="/demo" component={() => <Demo/>} />
          <Route path="*" component={() => <NotFound/>} />
        </Switch>
      </Router>
    </div>
  );
};
