"""Agregar modelos Sector y Mesa

Revision ID: e3aea5daada9
Revises: 63ae69fd644b
Create Date: 2025-11-05 12:33:43.214292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3aea5daada9'
down_revision = '63ae69fd644b'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla sector
    op.create_table(
        'sector',
        sa.Column('id_sector', sa.Integer(), nullable=False),
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('baja', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id_sector'),
        sa.UniqueConstraint('numero')
    )
    
    # Crear tabla mesa
    op.create_table(
        'mesa',
        sa.Column('id_mesa', sa.Integer(), nullable=False),
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('cant_comensales', sa.Integer(), nullable=False),
        sa.Column('id_sector', sa.Integer(), nullable=False),
        sa.Column('baja', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['id_sector'], ['sector.id_sector'], ),
        sa.PrimaryKeyConstraint('id_mesa'),
        sa.UniqueConstraint('numero')
    )


def downgrade():
    # Eliminar tabla mesa primero (por foreign key)
    op.drop_table('mesa')
    # Eliminar tabla sector
    op.drop_table('sector')
