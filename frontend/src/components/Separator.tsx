interface Props {
  char?: string;
}

export function Separator({ char = '\u2550' }: Props) {
  return <div className="separator">{char.repeat(200)}</div>;
}
