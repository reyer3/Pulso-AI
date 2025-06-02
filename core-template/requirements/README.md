# 🚀 Pulso-AI - Simplified Dependencies

Este proyecto usa **pyproject.toml** como único sistema de dependencias.

## ✅ Recommended Approach (Current)

```bash
# Install for development  
pip install -e .[dev]

# Install for production
pip install -e .[prod]

# Install only base dependencies
pip install -e .
```

## ❌ Deprecated Files (Being Removed)

- `requirements.txt` ← Generated freeze, causes conflicts
- `requirements/base.txt` ← Redundant with pyproject.toml  
- `requirements/dev.txt` ← Redundant with pyproject.toml
- `requirements/prod.txt` ← Redundant with pyproject.toml

## 🔄 Migration Guide

### For Development
```bash
# Old way
pip install -r requirements/dev.txt

# New way (recommended)
pip install -e .[dev]
```

### For Production  
```bash
# Old way
pip install -r requirements/prod.txt

# New way (recommended)
pip install -e .[prod]
```

### For Deployment (if needed)
```bash
# Generate exact versions for deployment
pip freeze > deployment-requirements.txt

# Use in deployment
pip install -r deployment-requirements.txt
```

## 🎯 Benefits

- ✅ **Single source of truth**: Only pyproject.toml
- ✅ **Modern tooling**: Compatible with pip, poetry, uv, etc.
- ✅ **Flexible ranges**: Allows compatible updates
- ✅ **Clear separation**: dev, prod, test dependencies
- ✅ **No conflicts**: Eliminates version contradictions

## 📚 Reference

- [PEP 621](https://peps.python.org/pep-0621/) - Storing project metadata in pyproject.toml
- [PyPA Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) - Writing pyproject.toml
