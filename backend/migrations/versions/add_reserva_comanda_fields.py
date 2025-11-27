"""Add estado field to Reserva, Mesa and id_reserva to Comanda

Revision ID: add_reserva_comanda_fields
Revises: 70c6a60ec674
Create Date: 2025-11-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_reserva_comanda_fields'
down_revision = '70c6a60ec674'
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna estado a reserva
    op.add_column('reserva', sa.Column('estado', sa.String(20), nullable=False, server_default='activa'))
    
    # Agregar columna estado a mesa
    op.add_column('mesa', sa.Column('estado', sa.String(20), nullable=False, server_default='disponible'))
    
    # Agregar columna id_reserva a comanda
    op.add_column('comanda', sa.Column('id_reserva', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_comanda_reserva', 'comanda', 'reserva', ['id_reserva'], ['id_reserva'])


def downgrade():
    # Remover las columnas y relaciones
    op.drop_constraint('fk_comanda_reserva', 'comanda', type_='foreignkey')
    op.drop_column('comanda', 'id_reserva')
    op.drop_column('mesa', 'estado')
    op.drop_column('reserva', 'estado')
