export interface Result {
  label: number;
  class: string;
  probabilities: {
    DR: number;
    NoDR: number;
  };
}
