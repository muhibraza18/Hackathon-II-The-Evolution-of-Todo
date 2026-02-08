"""Add advanced todo fields

Revision ID: 001
Revises:
Create Date: 2026-01-28 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel.sql.sqltypes
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to the task table
    op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('priority', sa.String(length=20), nullable=True))
    op.add_column('task', sa.Column('tags', sa.String(length=1000), nullable=True))
    op.add_column('task', sa.Column('recurring_config', sa.String(length=1000), nullable=True))
    op.add_column('task', sa.Column('next_occurrence_id', sa.String(length=100), nullable=True))
    op.add_column('task', sa.Column('parent_task_id', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('original_task_id', sa.Integer(), nullable=True))

    # Create indexes for new columns
    op.create_index(op.f('ix_task_due_date'), 'task', ['due_date'], unique=False)
    op.create_index(op.f('ix_task_priority'), 'task', ['priority'], unique=False)
    op.create_index(op.f('ix_task_next_occurrence_id'), 'task', ['next_occurrence_id'], unique=False)
    op.create_index(op.f('ix_task_parent_task_id'), 'task', ['parent_task_id'], unique=False)
    op.create_index(op.f('ix_task_original_task_id'), 'task', ['original_task_id'], unique=False)

    # Add foreign key constraints for parent_task_id and original_task_id
    op.create_foreign_key('fk_task_parent_task_id_task', 'task', 'task', ['parent_task_id'], ['id'])
    op.create_foreign_key('fk_task_original_task_id_task', 'task', 'task', ['original_task_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key constraints first
    op.drop_constraint('fk_task_original_task_id_task', 'task', type_='foreignkey')
    op.drop_constraint('fk_task_parent_task_id_task', 'task', type_='foreignkey')

    # Drop indexes
    op.drop_index(op.f('ix_task_original_task_id'), table_name='task')
    op.drop_index(op.f('ix_task_parent_task_id'), table_name='task')
    op.drop_index(op.f('ix_task_next_occurrence_id'), table_name='task')
    op.drop_index(op.f('ix_task_priority'), table_name='task')
    op.drop_index(op.f('ix_task_due_date'), table_name='task')

    # Drop columns
    op.drop_column('task', 'original_task_id')
    op.drop_column('task', 'parent_task_id')
    op.drop_column('task', 'next_occurrence_id')
    op.drop_column('task', 'recurring_config')
    op.drop_column('task', 'tags')
    op.drop_column('task', 'priority')
    op.drop_column('task', 'due_date')