import {
  createMuiTheme,
  responsiveFontSizes,
  Theme,
} from '@material-ui/core/styles';

export const theme: Theme = responsiveFontSizes(
  createMuiTheme({
    palette: {
      primary: {
        light: '#80cbc4',
        main: '#009688',
        dark: '#004d40',
      },
      background: {
        default: '#fff',
      },
    },
    overrides: {
      MuiButton: {
        text: {
          color: '#fff',
          backgroundColor: '#009688',
          '&:hover': {
            backgroundColor: '#004d40',
          },
        },
      },
    },
  })
);
