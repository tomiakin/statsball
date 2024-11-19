// Modal.js
import React, { useRef, useEffect } from 'react';

const Modal = ({ isOpen, onClose, title, children, footer }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = event => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();
      }
    };

    const handleEscapeKey = event => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscapeKey);
      // Prevent scroll when modal is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscapeKey);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50'
      role='dialog'
      aria-modal='true'
      aria-labelledby='modal-title'
    >
      <div
        ref={modalRef}
        className='w-full max-w-lg overflow-hidden rounded-lg bg-white shadow-lg'
      >
        <div className='flex items-center justify-between border-b p-4'>
          <h2 id='modal-title' className='text-xl font-semibold'>
            {title}
          </h2>
          <button
            className='rounded-full p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700'
            onClick={onClose}
            aria-label='Close modal'
          >
            ×
          </button>
        </div>
        <div className='p-6'>{children}</div>
        {footer && <div className='border-t p-4 text-right'>{footer}</div>}
      </div>
    </div>
  );
};

export default Modal;
