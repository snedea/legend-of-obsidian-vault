interface Props {
  char?: string;
  width?: number;
}

export function Separator({ char = '\u2550', width = 79 }: Props) {
  return <div className="separator">{char.repeat(width)}</div>;
}
