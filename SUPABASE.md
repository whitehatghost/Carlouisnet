# Conectar la app para que los tres vean lo mismo

Son unos 10 minutos, una sola vez. Después nadie vuelve a tocar esto.

Lo único que no puedo hacer yo es crear la cuenta: necesita su correo y su
contraseña, y esas no me las tiene que dar.

---

## 1. Crear el proyecto (3 min)

1. Entrá a <https://supabase.com> y tocá **Start your project**.
2. Entrá con GitHub o con correo. Es gratis y **no pide tarjeta**.
3. Tocá **New project**:
   - **Name**: `carlouis`
   - **Database Password**: poné una larga y **guardala** — no la va a volver
     a ver y sirve para recuperar la base si algo pasa.
   - **Region**: `East US (North Virginia)` — es la más cercana a Costa Rica.
4. Tocá **Create new project** y esperá un par de minutos a que termine.

## 2. Crear las tablas (1 min)

1. En el menú de la izquierda, **SQL Editor**.
2. Tocá **New query**.
3. Abrí el archivo `tools/supabase.sql` de este repositorio, copiá **todo** y
   pegalo ahí.
4. Tocá **Run** (o Ctrl+Enter).
5. Tiene que decir *Success*. Si sale algo en rojo, mandámelo y lo reviso.

## 3. Crear la cuenta del negocio (2 min)

Esta es **una sola cuenta que usan los tres**. No es la suya de Supabase: es
la que va a ir dentro de la app.

1. Menú izquierdo → **Authentication** → **Users**.
2. Tocá **Add user** → **Create new user**.
3. Poné:
   - **Email**: algo del negocio, por ejemplo `carlouis@carlouis.net`
     (no necesita existir de verdad).
   - **Password**: una que se pueda dictar por teléfono. Los tres la van a
     escribir una vez en su celular.
   - Marcá **Auto Confirm User**. Importante: si no se marca, no va a poder
     entrar.
4. Tocá **Create user**.

## 4. Pasarme los dos datos (1 min)

1. Menú izquierdo → **Project Settings** (el engranaje abajo) → **API**.
2. Copiame estos dos:
   - **Project URL** — se ve así: `https://abcdefgh.supabase.co`
   - **anon public** — una clave larga que empieza con `eyJ...`

**Esos dos son públicos por diseño**: van dentro de la app y cualquiera que
abra el código los puede ver. Lo que protege los datos son las reglas de
seguridad que ya quedaron puestas en el paso 2, no el secreto de la clave.

> **NUNCA me mande la que dice `service_role`.** Esa sí salta todas las
> reglas de seguridad y da acceso total a la base. Si alguna vez la comparte
> por error, entre a Supabase y tóquele **Reset**.

## 5. Yo conecto y listo

Con esos dos datos yo dejo la app conectada. Después, en cada celular:

1. Abrir la app.
2. Escribir el correo y la contraseña del paso 3, una sola vez.
3. Escoger quién es: Luis, Carlina o usted.

Desde ahí, lo que uno agregue lo ven los otros.

---

## Cómo va a funcionar

- **Sin señal la app sigue trabajando igual.** Se puede cobrar en la feria sin
  internet; cuando vuelve la señal, sube solo lo que falte.
- **Si dos tocan lo mismo a la vez**, gana el cambio más reciente. Para lo que
  hacen —cada quien cobra su venta, cada quien anota su cliente— eso no da
  problema, porque no se están editando la misma fila.
- **Nada se borra de verdad**: se marca como borrado para que el otro teléfono
  se entere. Si no, lo volvería a subir.
- **El respaldo sigue sirviendo** y conviene seguir bajándolo. Una base en la
  nube no reemplaza tener el archivo.

## Lo que cambia respecto a hoy

Hoy los datos están **solo en cada teléfono**. Con esto pasan a estar también
en un servidor en Estados Unidos, de una empresa que no somos nosotros.

Para un negocio de salsas eso es normal y es lo que usa casi todo el mundo.
Pero es un cambio real y por eso se lo digo: antes, si alguien quería ver esos
datos tenía que tener el teléfono en la mano.
