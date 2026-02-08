-- Create reminders table for Phase V - Redpanda Cloud Integration
-- This table stores scheduled reminders for tasks with due times

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    due_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed')),
    event_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    sent_at TIMESTAMPTZ,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0 CHECK (retry_count >= 0),
    UNIQUE(task_id)
);

-- Create index for efficient pending reminder queries
CREATE INDEX IF NOT EXISTS idx_reminders_due_time
  ON reminders(due_time)
  WHERE status = 'pending';

-- Create index for user pending reminder queries
CREATE INDEX IF NOT EXISTS idx_reminders_user_status
  ON reminders(user_id, status);

-- Add comments
COMMENT ON TABLE reminders IS 'Scheduled reminders for tasks with due times';
COMMENT ON COLUMN reminders.due_time IS 'UTC timestamp when reminder should trigger';
COMMENT ON COLUMN reminders.event_published IS 'Whether event was published to Redpanda Cloud';
COMMENT ON COLUMN reminders.status IS 'pending, sent, or failed';
COMMENT ON COLUMN reminders.sent_at IS 'When reminder was actually sent to user';

-- Verify table creation
SELECT 'Reminders table created successfully' AS status;
