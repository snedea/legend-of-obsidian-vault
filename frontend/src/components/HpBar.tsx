interface Props {
  current: number;
  max: number;
  width?: number;
  label?: string;
}

export function HpBar({ current, max, width = 10, label }: Props) {
  const pct = max > 0 ? current / max : 0;
  const filled = Math.round(pct * width);
  const empty = width - filled;
  const pctValue = Math.round(pct * 100);

  const bar = '\u2588'.repeat(Math.max(0, filled)) + '\u2591'.repeat(Math.max(0, empty));

  let colorClass = 'c-green';
  if (pct < 0.25) colorClass = 'c-red';
  else if (pct < 0.6) colorClass = 'c-yellow';

  return (
    <span>
      {label && <span className="c-accent">{label} </span>}
      <span className={colorClass}>{bar}</span>
      <span className="c-muted"> {pctValue}%</span>
      <span className="c-muted"> ({current}/{max})</span>
    </span>
  );
}
