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

