import * as Yup from 'yup';

export const mozoValidationSchema = Yup.object({
  dni: Yup.string()
    .required('El DNI es requerido')
    .matches(/^\d+$/, 'El DNI debe contener solo números'),
  nombre: Yup.string()
    .required('El nombre es requerido')
    .min(2, 'El nombre debe tener al menos 2 caracteres'),
  apellido: Yup.string()
    .required('El apellido es requerido')
    .min(2, 'El apellido debe tener al menos 2 caracteres'),
  domicilio: Yup.string()
    .required('El domicilio es requerido')
    .min(5, 'El domicilio debe tener al menos 5 caracteres'),
  telefono: Yup.string()
    .required('El teléfono es requerido')
    .matches(/^\d+$/, 'El teléfono debe contener solo números'),
  sector: Yup.string()
    .required('El sector es requerido')
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

