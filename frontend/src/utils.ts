export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) =>
  localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export function forceFileDownload(data: any, fileName: string) {
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', fileName);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export function getNestedValue(
  obj: any,
  path: (string | number)[],
  fallback?: any
): any {
  const last = path.length - 1;

  if (last < 0) return obj === undefined ? fallback : obj;

  for (let i = 0; i < last; i++) {
    if (obj == null) {
      return fallback;
    }
    obj = obj[path[i]];
  }

  if (obj == null) return fallback;

  return obj[path[last]] === undefined ? fallback : obj[path[last]];
}

export function getObjectValueByPath(
  obj: any,
  path: string,
  fallback?: any
): any {
  // credit: http://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key#comment55278413_6491621
  if (obj == null || !path || typeof path !== 'string') return fallback;
  if (obj[path] !== undefined) return obj[path];
  path = path.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
  path = path.replace(/^\./, ''); // strip a leading dot
  return getNestedValue(obj, path.split('.'), fallback);
}

export function defaultFilter(value: any, search: string | null, item: any) {
  return (
    value != null &&
    search != null &&
    typeof value !== 'boolean' &&
    value
      .toString()
      .toLocaleLowerCase()
      .indexOf(search.toLocaleLowerCase()) !== -1
  );
}
