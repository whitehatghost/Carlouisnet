/* Conexión a la base compartida.
 *
 * Estos dos datos son PÚBLICOS por diseño: van dentro de la app y cualquiera
 * que abra el código los puede leer. Lo que protege los datos son las reglas
 * de seguridad de la base (tools/supabase.sql), no el secreto de la llave.
 *
 * La llave que SÍ es secreta es la que dice "service_role". Esa nunca va acá
 * ni en ningún archivo de este repositorio.
 *
 * Mientras estén vacíos, la app funciona igual pero solo en este teléfono.
 * Ver SUPABASE.md para llenarlos.
 */
window.NUBE_CONFIG = {
  url: '',
  llave: ''
};
