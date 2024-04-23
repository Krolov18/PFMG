from dataclasses import dataclass


@dataclass
class Agreement:
    data: dict

    def from_string(
        self,
        accords: str,
        accumulator: list[dict] | dict
    ) -> None:
        if not accords:
            return

        if ":" in accords:
            for i_idx, i_x in enumerate(accords.split(";")):
                self.from_string(i_x, accumulator[i_idx])
        elif "," in accords:
            for x in accords.split(","):
                self.from_string(x, accumulator)
        elif "=" in accords:
            if not all(lhs_rhs := accords.partition("=")):
                raise TypeError(lhs_rhs)
            match accumulator:
                case [a]:
                    match a:
                        case {"Source": values}:
                            values[f"S{lhs_rhs[0]}"] = lhs_rhs[2]
                        case {"Destination": values}:
                            values[f"D{lhs_rhs[0]}"] = lhs_rhs[2]
                case {"Source": values}:
                    values[f"S{lhs_rhs[0]}"] = lhs_rhs[2]
                case {"Destination": values}:
                    values[f"D{lhs_rhs[0]}"] = lhs_rhs[2]
                case _:
                    raise TypeError(accords, accumulator)
        else:
            match accumulator:
                case [a]:
                    match a:
                        case {"Source": values}:
                            values[f"S{accords}"] = f"?S{accords}"
                        case {"Destination": values}:
                            values[f"D{accords}"] = f"?D{accords}"
                case {"Source": values}:
                    values[f"S{accords}"] = f"?S{accords}"
                case {"Destination": values}:
                    values[f"D{accords}"] = f"?D{accords}"
                case _:
                    raise TypeError(accords, accumulator)
