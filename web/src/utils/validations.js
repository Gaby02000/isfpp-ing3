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

