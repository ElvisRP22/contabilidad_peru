# Sistema Contable Perú - AGENTS.md

## Project Overview
- **Type**: Multi-tenant web accounting system for Peruvian public accountants/studios
- **Clients**: < 50 companies (small studio)
- **Tech Stack**: Python Django 5.x + React 18 + TypeScript + PostgreSQL (Docker)

## Architecture

```
contabilidad_peru/
├── backend/                    # Django REST API
│   ├── apps/
│   │   ├── core/              # Auth, Empresas, Tenant
│   │   ├── contabilidad/      # Plan de Cuentas, Asientos
│   │   ├── facturacion/        # CPE, XML, SUNAT
│   │   ├── inventario/         # Productos, Kárdex
│   │   └── nomina/            # Empleados, Planillas
│   └── contabilidad_peru/      # Settings
├── frontend/                   # React + TypeScript + Vite
│   └── src/
│       ├── pages/            # UI pages
│       ├── services/          # API client
│       └── stores/           # Zustand state
└── docker-compose.yml
```

## Key Developer Commands

```bash
# Start all services
docker-compose up --build

# Backend (individual)
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (individual)
cd frontend
npm install
npm run dev

# Create superuser
python manage.py createsuperuser
```

## API Endpoints

| Module | Endpoint | Description |
|--------|----------|-------------|
| Core | `/api/core/auth/login/` | JWT Login |
| Core | `/api/core/empresas/` | Companies |
| Contabilidad | `/api/contabilidad/plan-cuentas/` | Chart of accounts |
| Contabilidad | `/api/contabilidad/asientos/` | Journal entries |
| Facturación | `/api/facturacion/comprobantes/` | E-invoices |
| Inventario | `/api/inventario/productos/` | Products |
| Nómina | `/api/nomina/empleados/` | Employees |

## Peruvian Regulatory Requirements

### Facturación Electrónica (SUNAT)
- OSE/PSE integration required
- XML signing with digital certificate
- CPE types: 01-Factura, 03-Boleta, 07-Nota Crédito, 08-Nota Débito
- CDR (Constancia de Recepción) storage mandatory

### Contabilidad
- PCGE (Plan de Cuentas General Empresarial) structure
- Double-entry bookkeeping (partida doble)
- Validation: debe == haber for each entry
- PLE generation: monthly txt files for Sunat

### Nómina
- PLAME format for PDT 0611
- CTS, Gratificaciones, Essalud calculations

## Multi-Tenant Structure
- One Database (shared schema)
- `empresa` field on all financial models
- Middleware filters by current tenant
- `request.user.empresa` for tenant context

## Frontend Stack
- React 18 + TypeScript + Vite
- TanStack Query (data fetching)
- Zustand (state management)
- TailwindCSS (styling)
- Recharts (dashboard)

## Database Models

| App | Models |
|-----|--------|
| core | Usuario, Empresa, SerieDocumento, ParametroSistema |
| contabilidad | PlanCuenta, Asiento, DetalleAsiento, CentroCosto |
| facturacion | Comprobante, DetalleComprobante, HistorialEnvio |
| inventario | Producto, Almacen, Kardex, StockAlmacen |
| nomina | Empleado, Remuneracion, Descuento, Planilla |

## Environment Setup
```bash
# Backend .env (required)
DATABASE_URL=postgres://admin:cont123456@localhost:5432/contabilidad
SECRET_KEY=django-secret-key-change-in-production
DEBUG=True

# Frontend .env (optional)
VITE_API_URL=http://localhost:8000
```

## Database Setup (first run)
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Important Notes
- No migrations exist yet - run `makemigrations` before first deploy
- FACTURACION: Services for XML signing not implemented (stub only)
- Certificate digital files stored in `core.Empresa.certificado_digital`
- OSE integration uses token-based auth (`empresa.ose_token`)
- PLE generator script needed for monthly SUNAT files

## Known Issues
- `apps.facturacion/serializers.py` has duplicate `ComprobanteSerializer` class (line conflict)
- Some fields use Spanish names (`basic_salary` vs `salario_basico` in nomina/)
- `apps.nomina/views.py` uses unprefixed `models` import