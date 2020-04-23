import React from 'react';
import { Container, Typography } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { PieChart, Pie, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { ResultScreenProps } from '../../types';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      width: 'min(100%, 700px)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      border: `1px solid ${theme.palette.primary.main}`,
      borderRadius: theme.spacing(2)
    },
    title: {
      color: theme.palette.primary.main,
      margin: theme.spacing(2)
    }
  })
);

export const ResultScreen: React.FC<ResultScreenProps> = ({ result }) => {
  const classes = useStyles();

  if(!result)
    return <div>An error has occured.</div>
  
  const { probabilities: { NoDR, DR } } = result;
  const pieDataChart = [
    { name: 'No DR probability', probability: Math.round(NoDR*10000) / 100, fill: '#00c9b6' }, 
    { name: 'DR probability', probability: Math.round(DR*10000) / 100, fill: '#007F73' }
  ];

  return (
    <Container className={classes.root}>
      <Typography variant="h5" className={classes.title}>Prediction</Typography>
      <ResponsiveContainer width={'100%'} height={300}>
        <PieChart>
          <Pie isAnimationActive={true} data={pieDataChart} dataKey='probability' outerRadius={80} label>
            {pieDataChart.map((item, index) => <Cell key={index} fill={item.fill}/>)}
          </Pie>
          <Tooltip/>
          <Legend/>
        </PieChart>
      </ResponsiveContainer>
    </Container>
  );
}
