import React from 'react';
import { Camera, Mail, Phone, MapPin, Instagram, Facebook, Twitter, Linkedin } from 'lucide-react';

export function Footer() {
  return (
    <footer style={{
      backgroundColor: '#1E293B',
      color: '#FFFFFF',
      marginTop: 'auto'
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '4rem 2rem 2rem'
      }}>
        {/* Main Footer Content */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '3rem',
          marginBottom: '3rem'
        }}>
          {/* Brand Section */}
          <div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              marginBottom: '1.5rem'
            }}>
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
                letterSpacing: '-0.02em'
              }}>
                Culex
              </span>
            </div>
            <p style={{
              color: '#94A3B8',
              fontSize: '0.9375rem',
              lineHeight: '1.6',
              marginBottom: '1.5rem'
            }}>
              Connect with talented photographers for your perfect moment. Professional photography services at your fingertips.
            </p>
            <div style={{
              display: 'flex',
              gap: '1rem'
            }}>
              {[Instagram, Facebook, Twitter, Linkedin].map((Icon, index) => (
                <button
                  key={index}
                  style={{
                    width: '40px',
                    height: '40px',
                    backgroundColor: '#334155',
                    borderRadius: '8px',
                    border: 'none',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#2563EB';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = '#334155';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  <Icon size={18} color="#FFFFFF" />
                </button>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 style={{
              fontSize: '1rem',
              fontWeight: '600',
              marginBottom: '1.5rem',
              color: '#FFFFFF'
            }}>
              Quick Links
            </h4>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              {['Home', 'Find Photographers', 'How It Works', 'Pricing', 'About Us'].map((link) => (
                <li key={link}>
                  <button style={{
                    background: 'none',
                    border: 'none',
                    color: '#94A3B8',
                    fontSize: '0.9375rem',
                    cursor: 'pointer',
                    padding: 0,
                    transition: 'color 0.2s ease',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = '#FFFFFF'}
                  onMouseLeave={(e) => e.currentTarget.style.color = '#94A3B8'}
                  >
                    {link}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* For Photographers */}
          <div>
            <h4 style={{
              fontSize: '1rem',
              fontWeight: '600',
              marginBottom: '1.5rem',
              color: '#FFFFFF'
            }}>
              For Photographers
            </h4>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              {['Join as Photographer', 'Dashboard', 'Portfolio Management', 'Pricing Plans', 'Resources'].map((link) => (
                <li key={link}>
                  <button style={{
                    background: 'none',
                    border: 'none',
                    color: '#94A3B8',
                    fontSize: '0.9375rem',
                    cursor: 'pointer',
                    padding: 0,
                    transition: 'color 0.2s ease',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.color = '#FFFFFF'}
                  onMouseLeave={(e) => e.currentTarget.style.color = '#94A3B8'}
                  >
                    {link}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 style={{
              fontSize: '1rem',
              fontWeight: '600',
              marginBottom: '1.5rem',
              color: '#FFFFFF'
            }}>
              Contact Us
            </h4>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}>
              <li style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
                color: '#94A3B8',
                fontSize: '0.9375rem'
              }}>
                <Mail size={18} style={{ marginTop: '2px', flexShrink: 0 }} />
                <span>support@dekodak.com</span>
              </li>
              <li style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
                color: '#94A3B8',
                fontSize: '0.9375rem'
              }}>
                <Phone size={18} style={{ marginTop: '2px', flexShrink: 0 }} />
                <span>+31 20 123 4567</span>
              </li>
              <li style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
                color: '#94A3B8',
                fontSize: '0.9375rem',
                lineHeight: '1.5'
              }}>
                <MapPin size={18} style={{ marginTop: '2px', flexShrink: 0 }} />
                <span>Amsterdam, Netherlands</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div style={{
          paddingTop: '2rem',
          borderTop: '1px solid #334155',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <p style={{
            color: '#94A3B8',
            fontSize: '0.875rem',
            margin: 0
          }}>
            © 2024 Culex. All rights reserved.
          </p>
          <div style={{
            display: 'flex',
            gap: '2rem'
          }}>
            {['Privacy Policy', 'Terms of Service', 'Cookie Policy'].map((link) => (
              <button
                key={link}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#94A3B8',
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                  padding: 0,
                  transition: 'color 0.2s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.color = '#FFFFFF'}
                onMouseLeave={(e) => e.currentTarget.style.color = '#94A3B8'}
              >
                {link}
              </button>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}