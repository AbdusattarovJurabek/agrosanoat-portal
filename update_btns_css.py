import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

old_btns = """.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(255,255,255,0.2), transparent);
  opacity: 0;
  transition: var(--transition-normal);
}

.btn:hover::after { opacity: 1; }

.btn-primary {
  background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-700) 100%);
  color: #ffffff;
  box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
  border: 1px solid rgba(255,255,255,0.1);
}

.btn-primary:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 15px 30px -5px rgba(16, 185, 129, 0.5);
}

.btn-secondary {
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.btn-secondary:hover {
  background: var(--bg-card);
  border-color: var(--primary-400);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.btn-accent {
  background: linear-gradient(135deg, var(--accent-amber) 0%, var(--accent-gold) 100%);
  color: #ffffff;
  box-shadow: 0 10px 20px -5px rgba(245, 158, 11, 0.4);
  border: 1px solid rgba(255,255,255,0.1);
}

.btn-accent:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 15px 30px -5px rgba(245, 158, 11, 0.5);
}"""

new_btns = """.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.05);
  opacity: 0;
  transition: var(--transition-fast);
}

.btn:hover::after { opacity: 1; }

.btn-primary {
  background: rgba(0, 210, 106, 0.1);
  color: var(--primary-600);
  border: 1px solid var(--primary-600);
  box-shadow: inset 0 0 10px rgba(0, 210, 106, 0.1);
}

.btn-primary:hover {
  background: var(--primary-600);
  color: #0B0F19;
  box-shadow: 0 0 15px rgba(0, 210, 106, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

.btn-accent {
  background: transparent;
  color: var(--accent-amber);
  border: 1px solid var(--accent-amber);
}

.btn-accent:hover {
  background: var(--accent-amber);
  color: #0B0F19;
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
}"""

if old_btns in content:
    content = content.replace(old_btns, new_btns)
    with open("css/styles.css", "w", encoding="utf-8") as f:
        f.write(content)
    print("styles.css buttons updated to Tech Theme")
else:
    print("Could not find exact buttons section text to replace.")
