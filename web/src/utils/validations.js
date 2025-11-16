import * as Yup from 'yup';


export const mozoValidationSchema = Yup.object().shape({
  documento: Yup.string()
    .required('El DNI es requerido'),
  nombre_apellido: Yup.string()
    .required('El nombre es requerido'),
  direccion: Yup.string()
    .required('El domicilio es requerido'),
  telefono: Yup.string()
    .required('El teléfono es requerido')
    .matches(/^\d{7,15}$/, 'Debe ser un número válido'),
  id_sector: Yup.string()
    .required('El sector es requerido'),
});

export const mesaValidationSchema = Yup.object({
  numero: Yup.number()
    .required('El número de mesa es requerido')
    .positive('El número debe ser positivo')
    .integer('El número debe ser un entero'),
  tipo: Yup.string()
    .required('El tipo de mesa es requerido')
    .min(2, 'El tipo debe tener al menos 2 caracteres'),
  cant_comensales: Yup.number()
    .required('La cantidad de comensales es requerida')
    .positive('La cantidad debe ser positiva')
    .integer('La cantidad debe ser un número entero'),
  id_sector: Yup.number()
    .required('El sector es requerido')
    .positive('Debe seleccionar un sector')
});

export const sectorValidationSchema = Yup.object({
  numero: Yup.number()
    .required('El número de sector es requerido')
    .positive('El número debe ser positivo')
    .integer('El número debe ser un entero')
});

export const clienteValidationSchema = Yup.object({
  documento: Yup.string()
    .required('El documento es obligatorio')
    .matches(/^[0-9]+$/, "El documento debe contener solo números")
    .min(7, 'Debe tener al menos 7 dígitos')
    .max(50, 'Máximo 50 caracteres'), // Límite de tu modelo
  
  nombre: Yup.string()
    .required('El nombre es obligatorio')
    .min(2, 'El nombre debe tener al menos 2 caracteres')
    .max(100, 'Máximo 100 caracteres'), // Límite de tu modelo

  apellido: Yup.string()
    .required('El apellido es obligatorio')
    .min(2, 'El apellido debe tener al menos 2 caracteres')
    .max(100, 'Máximo 100 caracteres'), // Límite de tu modelo

  num_telefono: Yup.string()
    .required('El teléfono es obligatorio')
    .matches(/^[0-9]+$/, 'El teléfono debe contener solo números')
    .max(50, 'Máximo 50 caracteres'), // Límite de tu modelo

  email: Yup.string()
    .email('Formato de email inválido')
    .required('El email es obligatorio')
    .max(100, 'Máximo 100 caracteres'), // Límite de tu modelo
});
export const productoValidationSchema = Yup.object({
  nombre: Yup.string()
    .required('El nombre es obligatorio')
    .max(255, 'Máximo 255 caracteres'),
  codigo: Yup.string()
    .required('El código es obligatorio')
    .max(50, 'Máximo 50 caracteres'),
  precio: Yup.number()
    .typeError('El precio debe ser un número')
    .positive('Debe ser mayor a 0')
    .required('El precio es obligatorio'),
  id_seccion: Yup.number()
    .typeError('Debe seleccionar una sección')
    .required('Debe seleccionar una sección'),
  descripcion: Yup.string()
    .max(500, 'Máximo 500 caracteres')
    .nullable(),
});

export const seccionValidationSchema = Yup.object({
  nombre: Yup.string()
    .required('El nombre de la sección es obligatorio')
    .max(255, 'Máximo 255 caracteres'),
  baja: Yup.boolean().nullable(),
});

export const medioPagoValidationSchema = Yup.object({
  nombre: Yup.string()
    .required('El nombre del medio de pago es obligatorio') 
    .max(100, 'Máximo 100 caracteres'),
  descripcion: Yup.string()
    .max(255, 'Máximo 255 caracteres')
    .nullable(),
});
