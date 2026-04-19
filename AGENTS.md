# Sistema Contable Perú - AGENTS.md

## Project Overview
- **Type**: Multi-tenant web accounting system for Peruvian public accountants/studios
- **Clients**: < 50 companies (small studio)
- **Tech Stack**: Python Django 5.x + React 18 + TypeScript + PostgreSQL (Docker)
- **Regulatory**: SUNAT (facturación electrónica), PLE, PLAME

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
└── docker-compose.yml
```

## Key Developer Commands

```bash
# Start all services
docker-compose up --build

# Backend (individual)
cd backend
pip install -r requirements.txt
python manage.py makemigrations  # RUN FIRST TIME
python manage.py migrate
python manage.py runserver

# Frontend (individual)
cd frontend
npm install
npm run dev

# Create superuser
python manage.py createsuperuser
```

## Database Tables

### core (Usuario y Empresa)
| Table | Description |
|-------|------------|
| core_usuario | Users (extends AbstractUser) |
| core_empresa | Companies (tenant) |
| core_serie_documento | Document series config |
| core_parametro | System parameters |

### contabilidad (Contabilidad)
| Table | Description |
|-------|------------|
| contabilidad_plan_cuenta | Chart of accounts (PCGE) |
| contabilidad_asiento | Journal entries |
| contabilidad_detalle_asiento | Entry lines |
| contabilidad_centro_costo | Cost centers |

### facturacion (Facturación Electrónica)
| Table | Description |
|-------|------------|
| facturacion_comprobante | CPE (01,03,07,08) |
| facturacion_detalle_comprobante | CPE line items |
| facturacion_documento_referencia | References (NC/ND) |
| facturacion_historial_envio | Send history |

### inventario (Inventario)
| Table | Description |
|-------|------------|
| inventario_almacen | Warehouses |
| inventario_categoria | Categories |
| inventario_producto | Products |
| inventario_kardex | Stock movements |
| inventario_stock_almacen | Stock per warehouse |

### nomina (Nómina)
| Table | Description |
|-------|------------|
| nomina_empleado | Employees |
| nomina_remuneracion | Monthly earnings |
| nomina_descuento | Monthly deductions |
| nomina_beneficio | Social benefits (CTS,Grat) |
| nomina_asistencia | Attendance |
| nomina_planilla | Monthly payroll |

## REST API Endpoints

### Core - Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/core/auth/login/` | JWT Login |
| POST | `/api/core/auth/refresh/` | Refresh token |

### Core - Usuarios
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/core/usuarios/` | List/Create |
| GET/PUT/DELETE | `/api/core/usuarios/{id}/` | CRUD |

### Core - Empresas
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/core/empresas/` | List/Create |
| GET/PUT/DELETE | `/api/core/empresas/{id}/` | CRUD |
| GET | `/api/core/empresas/{id}/series/` | Get series |
| POST | `/api/core/empresas/{id}/agregar_serie/` | Add series |

### Contabilidad
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/contabilidad/plan-cuentas/` | List/Create accounts |
| GET/PUT/DELETE | `/api/contabilidad/plan-cuentas/{id}/` | CRUD |
| GET/POST | `/api/contabilidad/asientos/` | List/Create entries |
| POST | `/api/contabilidad/asientos/{id}/aprobar/` | Approve |
| POST | `/api/contabilidad/asientos/{id}/cerrar/` | Close |
| GET | `/api/contabilidad/reportes/balance_comprobacion/?fecha=` | Balance |
| GET | `/api/contabilidad/reportes/mayor/?cuenta_id=&fecha_inicio=&fecha_fin=` | Mayor |

### Facturación
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/facturacion/comprobantes/` | List/Create CPE |
| POST | `/api/facturacion/comprobantes/{id}/generar/` | Generate XML |
| POST | `/api/facturacion/comprobantes/{id}/firmar/` | Sign XML |
| POST | `/api/facturacion/comprobantes/{id}/enviar_sunat/` | Send to SUNAT |
| GET | `/api/facturacion/comprobantes/{id}/obtener_pdf/` | Get PDF |
| POST | `/api/facturacion/comprobantes/{id}/anular/` | Void CPE |

### Inventario
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/inventario/almacenes/` | Warehouses |
| GET/POST | `/api/inventario/categorias/` | Categories |
| GET/POST | `/api/inventario/productos/` | Products |
| GET/POST | `/api/inventario/kardex/` | Stock movements |
| GET | `/api/inventario/productos/{id}/kardex/?desde=&hasta=` | Product kardex |

### Nómina
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/nomina/empleados/` | Employees |
| GET/POST | `/api/nomina/planillas/` | Payrolls |
| POST | `/api/nomina/planillas/{id}/generar_planilla/` | Generate details |
| GET | `/api/nomina/planillas/{id}/generar_plame/` | Export PLAME |

## Business Rules

### Contabilidad
- **Partida doble**: debe == haber required for every entry
- Only level 6 accounts can have movements (`cuenta.acepta_movimiento=True`)
- Entries must be approved before closing
- Closed entries cannot be modified

### Facturación
- States: borrador → generado → firmado → enviado → aceptado → anulado
- Client RUC (6): show IGV; Client DNI (1): no IGV
- NC (07) / ND (08) require `referencia_documento`
- CDR must be stored for every SUNAT response

### Inventario
- PEPS / Promedio costing methods
- Stock cannot go negative unless `permite_stock_negativo=True`
- Every movement updates kardex automatically

### Nómina
- AFP: 10% aporte + 0.5% prima + 1.35% seguro
- CTS: 50% basic + 50% promedio / 12
- Gratificación: 100% basic (Jul/Dic)

## Multi-Tenant Structure
- One database (shared schema)
- `empresa` FK on all financial models
- TenantMiddleware filters by `request.user.empresa`
- Use `request.user.empresa` for tenant context

## Environment Setup
```bash
# Backend .env
DATABASE_URL=postgres://admin:cont123456@localhost:5432/contabilidad
SECRET_KEY=django-secret-key-change-in-production
DEBUG=True
POSTGRES_HOST=localhost
POSTGRES_DB=contabilidad
POSTGRES_USER=admin
POSTGRES_PASSWORD=cont123456

# Frontend .env (optional)
VITE_API_URL=http://localhost:8000
```

## Important Notes
- Run `makemigrations` before first deploy - no migrations exist
- FACTURACION: XML signing services are stubs (implement with xmlsec)
- Certificate digital files stored in `core.Empresa.certificado_digital`
- OSE uses token-based auth (`empresa.ose_token`)
- PLE generator script needed for monthly SUNAT files

## Testing Commands
```bash
# Backend
cd backend
pip install pytest pytest-django pytest-cov
pytest --cov=apps --cov-report=html

# Frontend
cd frontend
npm run test
```

## Known Issues
- apps.facturacion/serializers.py has duplicate class (fix required)
- Some fields use Spanish names in nomina models
- Apps need migration files created before use