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
        <div className="screen-content">
          {children}
        </div>
        {subtitle && <span className="border-subtitle">{subtitle}</span>}
      </div>
    </div>
  );
}
