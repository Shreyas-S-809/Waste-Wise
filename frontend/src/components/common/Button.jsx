export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  full = false,
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  ...rest
}) {
  const classes = [
    'btn',
    `btn--${variant}`,
    size !== 'md' ? `btn--${size}` : '',
    full ? 'btn--full' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled || loading}
      {...rest}
    >
      {loading && <span className="btn__spinner" />}
      {children}
    </button>
  );
}
