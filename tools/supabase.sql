-- ===========================================================================
-- CARLOUIS Control — base compartida
--
-- Se pega COMPLETO en Supabase → "SQL Editor" → "New query" → Run.
-- Se corre una sola vez. Si se corre dos veces no pasa nada.
--
-- Por qué una sola tabla y no siete: los datos de este negocio son pocos
-- —cientos de filas, no millones— y con una tabla genérica el código de
-- sincronización es uno solo en vez de siete. Menos código es menos que se
-- pueda romper cuando alguien esté cobrando en una feria sin señal.
-- ===========================================================================

create table if not exists public.datos (
  id          text primary key,
  negocio     uuid        not null default auth.uid(),
  tipo        text        not null,   -- cliente, pedido, gasto, ruta, feria, recordatorio, stock
  contenido   jsonb       not null,
  actualizado timestamptz not null default now(),
  borrado     boolean     not null default false,
  por         text                    -- quién lo tocó de último, para saber
);

-- Para traer solo lo que cambió desde la última vez.
create index if not exists datos_por_negocio
  on public.datos (negocio, actualizado desc);

-- ===========================================================================
-- SEGURIDAD
--
-- Esto es lo que impide que cualquiera con la llave pública lea las ventas.
-- La llave "anon" de Supabase va dentro de la app y por diseño es pública;
-- lo que protege los datos son estas reglas, no la llave.
--
-- Cada fila queda atada a la cuenta que la creó. Solo esa cuenta la ve.
-- ===========================================================================

alter table public.datos enable row level security;

drop policy if exists datos_ver     on public.datos;
drop policy if exists datos_crear   on public.datos;
drop policy if exists datos_cambiar on public.datos;

create policy datos_ver on public.datos
  for select using (negocio = auth.uid());

create policy datos_crear on public.datos
  for insert with check (negocio = auth.uid());

create policy datos_cambiar on public.datos
  for update using (negocio = auth.uid())
           with check (negocio = auth.uid());

-- No hay política de DELETE a propósito: nada se borra de verdad, se marca
-- borrado = true. Así el borrado también se sincroniza; si se borrara la
-- fila, el otro teléfono nunca se enteraría y la volvería a subir.

-- ===========================================================================
-- Marca la hora sola en cada cambio. Sin esto habría que confiar en el reloj
-- del teléfono, y dos teléfonos con la hora distinta se pisarían los datos.
-- ===========================================================================

create or replace function public.marcar_hora()
returns trigger language plpgsql as $$
begin
  new.actualizado = now();
  return new;
end $$;

drop trigger if exists datos_hora on public.datos;
create trigger datos_hora
  before insert or update on public.datos
  for each row execute function public.marcar_hora();

-- Listo. Si no salió nada en rojo, la base ya está.
