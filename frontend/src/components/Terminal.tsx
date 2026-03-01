import type { ReactNode } from 'react';

interface Props {
  title?: string;
  subtitle?: string;
  children: ReactNode;
}

export function Terminal({ title, subtitle, children }: Props) {
  return (
    <div className="terminal">
      <div className="screen-border">
        {title && <span className="border-title">{title}</span>}
        {subtitle && <span className="border-subtitle">{subtitle}</span>}
        {children}
      </div>
    </div>
  );
}
