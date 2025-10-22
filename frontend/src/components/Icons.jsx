import React from 'react';
import { FaPaperPlane, FaSpinner } from 'react-icons/fa'; // Using react-icons library

export const SendIcon = () => <FaPaperPlane className="inline-block ml-1" />;

export const LoaderIcon = () => (
  <FaSpinner className="animate-spin inline-block text-gray-500" />
);
