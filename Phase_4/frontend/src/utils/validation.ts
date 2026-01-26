interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

interface LoginData {
  email: string;
  password: string;
}

interface RegistrationData extends LoginData {
  name?: string;
}

/**
 * Validate login form data
 */
export const validateLogin = (email: string, password: string): ValidationResult => {
  const errors: Record<string, string> = {};

  // Validate email
  if (!email) {
    errors.email = 'Email is required';
  } else if (!/\S+@\S+\.\S+/.test(email)) {
    errors.email = 'Email is invalid';
  }

  // Validate password
  if (!password) {
    errors.password = 'Password is required';
  } else if (password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

/**
 * Validate registration form data
 */
export const validateRegistration = (email: string, password: string, name?: string): ValidationResult => {
  const errors: Record<string, string> = {};

  // Validate name (optional but if provided, must be valid)
  if (name && name.trim().length > 0 && name.trim().length < 2) {
    errors.name = 'Name must be at least 2 characters';
  }

  // Validate email
  if (!email) {
    errors.email = 'Email is required';
  } else if (!/\S+@\S+\.\S+/.test(email)) {
    errors.email = 'Email is invalid';
  }

  // Validate password
  if (!password) {
    errors.password = 'Password is required';
  } else if (password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(password)) {
    errors.password = 'Password must contain uppercase, lowercase, number, and special character';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};