import {
  createMuiTheme,
  responsiveFontSizes,
  Theme,
} from "@material-ui/core/styles";

export const theme: Theme = responsiveFontSizes(
  createMuiTheme({
    palette: {
      primary: {
        light: "#64b5f6",
        main: "#2196f3",
        dark: "#1976d2",
      },
      background: {
        default: "#fff",
      },
    },
  })
);