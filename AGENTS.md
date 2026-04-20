# Sistema Contable Perú - AGENTS.md

## Project Overview
- **Type**: Multi-tenant web accounting system for Peruvian public accountants/studios
- **Clients**: < 50 companies (small studio)
- **Tech Stack**: Python FastAPI + React 18 + TypeScript + PostgreSQL (Docker)
- **Regulatory**: SUNAT (facturación electrónica), PLE, PLAME

## Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings
│   ├── database.py             # SQLModel connection
│   ├── auth/                   # JWT authentication
│   ├── core/                   # Users, Companies
│   ├── contabilidad/           # Chart of accounts, Journal entries
│   ├── facturacion/            # CPE, XML, SUNAT
│   ├── inventario/             # Products, Stock
│   └── nomina/                 # Employees, Payroll
├── Dockerfile
└── requirements.txt
frontend/                        # React + TypeScript + Vite
```

## Key Developer Commands

```bash
# Start all services
docker-compose up --build

# Backend (individual)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (individual)
cd frontend
npm install
npm run dev
```

## Database Tables

### core (Usuario y Empresa)
| Table | Description |
|-------|------------|
| core_usuario | Users |
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

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | JWT Login |
| POST | `/api/auth/refresh` | Refresh token |
| GET | `/api/auth/me` | Current user |

### Core - Usuarios
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/core/usuarios` | List/Create |
| GET/PUT/DELETE | `/api/core/usuarios/{id}` | CRUD |

### Core - Empresas
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/core/empresas` | List/Create |
| GET/PUT/DELETE | `/api/core/empresas/{id}` | CRUD |
| GET | `/api/core/empresas/{id}/series` | Get series |
| POST | `/api/core/empresas/{id}/series` | Add series |

### Contabilidad
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/contabilidad/plan-cuentas` | List/Create accounts |
| GET/PUT/DELETE | `/api/contabilidad/plan-cuentas/{id}` | CRUD |
| GET/POST | `/api/contabilidad/asientos` | List/Create entries |
| GET | `/api/contabilidad/asientos/{id}` | Get entry |
| POST | `/api/contabilidad/asientos/{id}/aprobar` | Approve |
| POST | `/api/contabilidad/asientos/{id}/cerrar` | Close |
| GET | `/api/contabilidad/reportes/balance_comprobacion` | Balance |
| GET | `/api/contabilidad/reportes/mayor` | Mayor |

### Facturación
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/facturacion/comprobantes` | List/Create CPE |
| GET | `/api/facturacion/comprobantes/{id}` | Get CPE |
| POST | `/api/facturacion/comprobantes/{id}/generar` | Generate XML |
| POST | `/api/facturacion/comprobantes/{id}/firmar` | Sign XML |
| POST | `/api/facturacion/comprobantes/{id}/enviar_sunat` | Send to SUNAT |
| GET | `/api/facturacion/comprobantes/{id}/obtener_pdf` | Get PDF |
| POST | `/api/facturacion/comprobantes/{id}/anular` | Void CPE |

### Inventario
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/inventario/almacenes` | Warehouses |
| GET/POST | `/api/inventario/categorias` | Categories |
| GET/POST | `/api/inventario/productos` | Products |
| GET/PUT/DELETE | `/api/inventario/productos/{id}` | CRUD |
| GET | `/api/inventario/productos/{id}/kardex` | Product kardex |
| POST | `/api/inventario/kardex` | Create movement |

### Nómina
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/nomina/empleados` | Employees |
| GET/PUT/DELETE | `/api/nomina/empleados/{id}` | CRUD |
| GET/POST | `/api/nomina/planillas` | Payrolls |
| POST | `/api/nomina/planillas/{id}/generar_planilla` | Generate details |
| GET | `/api/nomina/planillas/{id}/generar_plame` | Export PLAME |

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
- Use `current_user.empresa_id` for tenant context

## Environment Setup
```bash
# Backend .env
DATABASE_URL=postgresql://admin:cont123456@localhost:5432/contabilidad
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend .env (optional)
VITE_API_URL=http://localhost:8000
```

## Testing Commands
```bash
# Backend
cd backend
pip install pytest pytest-cov
pytest --cov=app --cov-report=html

# Frontend
cd frontend
npm run test
```

## Known Issues
- XML signing services are stubs (implement with xmlsec)
- Certificate digital files stored in `core_empresa.certificado_digital`
- OSE uses token-based auth (`empresa.ose_token`)
- PLE generator script needed for monthly SUNAT files

## Dependencies

### Backend (requirements.txt)
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlmodel==0.0.20
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.9.2
pydantic-settings==2.5.2
```

### Frontend
- React 18 + TypeScript
- Vite (dev server)
- Axios (HTTP client)
- Zustand (state management)
- React Router DOM

## Running the Application

```bash
# Development with Docker
docker-compose up --build

# Or individual services:
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Access points:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs