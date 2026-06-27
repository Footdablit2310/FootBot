export class ValueIsNullError extends Error {
  constructor() {
    super("Value is null");
    this.name = "ValueIsNullError";
  }
}