import React from 'react';
import { Camera } from 'lucide-react';

interface HeaderProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export const Header = ({ currentPage, onNavigate }: HeaderProps) => {
  return (
    <header style={{
      backgroundColor: '#FFFFFF',
      borderBottom: '1px solid #E2E8F0',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)'
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '1rem 2rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Logo */}
        <button
          onClick={() => onNavigate('home')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '0.5rem'
          }}
        >
          <div style={{
            width: '40px',
            height: '40px',
            backgroundColor: '#1E3A8A',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Camera size={24} color="#FFFFFF" />
          </div>
          <span style={{
            fontSize: '1.5rem',
            fontWeight: '700',
            color: '#1E293B',
            letterSpacing: '-0.02em'
          }}>
            De Kodak
          </span>
        </button>

        {/* Navigation */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2rem'
        }}>
          <button
            onClick={() => onNavigate('home')}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: currentPage === 'home' ? '600' : '500',
              color: currentPage === 'home' ? '#2563EB' : '#475569',
              padding: '0.5rem 0',
              position: 'relative',
              transition: 'color 0.2s ease',
              borderBottom: currentPage === 'home' ? '2px solid #2563EB' : '2px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (currentPage !== 'home') e.currentTarget.style.color = '#2563EB';
            }}
            onMouseLeave={(e) => {
              if (currentPage !== 'home') e.currentTarget.style.color = '#475569';
            }}
          >
            Home
          </button>
          
          <button
            onClick={() => onNavigate('photographers')}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: currentPage === 'photographers' ? '600' : '500',
              color: currentPage === 'photographers' ? '#2563EB' : '#475569',
              padding: '0.5rem 0',
              transition: 'color 0.2s ease',
              borderBottom: currentPage === 'photographers' ? '2px solid #2563EB' : '2px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (currentPage !== 'photographers') e.currentTarget.style.color = '#2563EB';
            }}
            onMouseLeave={(e) => {
              if (currentPage !== 'photographers') e.currentTarget.style.color = '#475569';
            }}
          >
            Find Photographers
          </button>
          
          <button
            onClick={() => onNavigate('dashboard')}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: currentPage === 'dashboard' ? '600' : '500',
              color: currentPage === 'dashboard' ? '#2563EB' : '#475569',
              padding: '0.5rem 0',
              transition: 'color 0.2s ease',
              borderBottom: currentPage === 'dashboard' ? '2px solid #2563EB' : '2px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (currentPage !== 'dashboard') e.currentTarget.style.color = '#2563EB';
            }}
            onMouseLeave={(e) => {
              if (currentPage !== 'dashboard') e.currentTarget.style.color = '#475569';
            }}
          >
            Dashboard
          </button>

          <button
            onClick={() => onNavigate('bookings')}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: currentPage === 'bookings' ? '600' : '500',
              color: currentPage === 'bookings' ? '#2563EB' : '#475569',
              padding: '0.5rem 0',
              transition: 'color 0.2s ease',
              borderBottom: currentPage === 'bookings' ? '2px solid #2563EB' : '2px solid transparent'
            }}
            onMouseEnter={(e) => {
              if (currentPage !== 'bookings') e.currentTarget.style.color = '#2563EB';
            }}
            onMouseLeave={(e) => {
              if (currentPage !== 'bookings') e.currentTarget.style.color = '#475569';
            }}
          >
            My Bookings
          </button>

          <div style={{ 
            width: '1px', 
            height: '24px', 
            backgroundColor: '#E2E8F0' 
          }} />

          <button
            onClick={() => onNavigate('login')}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: '500',
              color: '#475569',
              padding: '0.5rem 1rem',
              transition: 'color 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = '#2563EB'}
            onMouseLeave={(e) => e.currentTarget.style.color = '#475569'}
          >
            Sign In
          </button>
          
          <button
            onClick={() => onNavigate('register')}
            style={{
              backgroundColor: '#2563EB',
              color: '#FFFFFF',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              fontWeight: '600',
              padding: '0.625rem 1.5rem',
              borderRadius: '0.75rem',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#1E40AF';
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#2563EB';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            Get Started
          </button>
        </nav>
      </div>
    </header>
  );
}