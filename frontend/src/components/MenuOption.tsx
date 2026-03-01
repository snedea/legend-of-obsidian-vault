interface Props {
  shortcut: string;
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export function MenuOption({ shortcut, label, onClick, disabled }: Props) {
  return (
    <button
      className="menu-option"
      onClick={onClick}
      disabled={disabled}
    >
      <span className="shortcut">({shortcut})</span> {label}
    </button>
  );
}
