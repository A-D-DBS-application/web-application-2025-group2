import React from 'react';
import { Search, Camera, Calendar, CheckCircle, Star, ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <div style={{ backgroundColor: '#FFFFFF' }}>
      {/* Hero Section */}
      <section style={{
        position: 'relative',
        minHeight: '700px',
        display: 'flex',
        alignItems: 'center',
        overflow: 'hidden',
        backgroundColor: '#FFFFFF'
      }}>
        <div style={{
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '6rem 2rem',
          width: '100%',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '6rem',
          alignItems: 'center'
        }}>
          {/* Hero Content */}
          <div>
            {/* Title */}
            <h1 style={{
              fontSize: '4rem',
              fontWeight: '800',
              color: '#1E293B',
              marginBottom: '2rem',
              lineHeight: '1.1',
              letterSpacing: '-0.02em'
            }}>
              About You
            </h1>

            {/* Subtitle */}
            <h2 style={{
              fontSize: '1.5rem',
              fontWeight: '600',
              color: '#475569',
              marginBottom: '1.5rem',
              lineHeight: '1.5'
            }}>
              You're a photographer who wants more time for your craft — not for emails, planning, or repetitive admin work.
            </h2>

            {/* Description */}
            <p style={{
              fontSize: '1.125rem',
              fontWeight: '400',
              color: '#64748B',
              marginBottom: '3rem',
              lineHeight: '1.7'
            }}>
              That's why we built an intelligent booking algorithm that automates your schedule, manages client requests, and sends confirmations. So you can focus on what truly matters: creating.
            </p>

            {/* Buttons Group */}
            <div style={{
              display: 'flex',
              gap: '1rem',
              flexWrap: 'wrap'
            }}>
              {/* Button Primary */}
              <button
                style={{
                  backgroundColor: '#2563EB',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '12px',
                  padding: '1rem 2rem',
                  fontSize: '1.0625rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 4px 12px rgba(37, 99, 235, 0.3)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#1E40AF';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 8px 20px rgba(37, 99, 235, 0.4)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#2563EB';
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
                }}
              >
                Learn More
              </button>

              {/* Button Secondary */}
              <button
                style={{
                  backgroundColor: 'transparent',
                  color: '#2563EB',
                  border: '2px solid #2563EB',
                  borderRadius: '12px',
                  padding: '1rem 2rem',
                  fontSize: '1.0625rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#EFF6FF';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                }}
              >
                How It Works
              </button>
            </div>
          </div>

          {/* Dashboard/Calendar Mockup */}
          <div style={{
            position: 'relative',
            borderRadius: '16px',
            overflow: 'hidden',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.1)',
            border: '1px solid #E2E8F0',
            backgroundColor: '#F8FAFC'
          }}>
            {/* Simple Dashboard Mockup */}
            <div style={{
              padding: '2rem',
              backgroundColor: '#FFFFFF'
            }}>
              {/* Header */}
              <div style={{
                marginBottom: '1.5rem',
                paddingBottom: '1rem',
                borderBottom: '1px solid #E2E8F0'
              }}>
                <div style={{
                  fontSize: '1.125rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.5rem'
                }}>
                  Your Schedule
                </div>
                <div style={{
                  fontSize: '0.875rem',
                  color: '#64748B'
                }}>
                  November 2025
                </div>
              </div>

              {/* Calendar Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(7, 1fr)',
                gap: '0.5rem',
                marginBottom: '1.5rem'
              }}>
                {['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'].map((day, i) => (
                  <div key={i} style={{
                    fontSize: '0.75rem',
                    fontWeight: '600',
                    color: '#64748B',
                    textAlign: 'center',
                    padding: '0.5rem'
                  }}>
                    {day}
                  </div>
                ))}
                {Array.from({ length: 28 }, (_, i) => i + 1).map((day) => (
                  <div key={day} style={{
                    aspectRatio: '1',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.875rem',
                    fontWeight: '500',
                    color: '#1E293B',
                    backgroundColor: [5, 12, 18, 23].includes(day) ? '#2563EB' : '#F8FAFC',
                    color: [5, 12, 18, 23].includes(day) ? '#FFFFFF' : '#1E293B',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}>
                    {day}
                  </div>
                ))}
              </div>

              {/* Upcoming Bookings */}
              <div>
                <div style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.75rem'
                }}>
                  Upcoming Bookings
                </div>
                {[
                  { client: 'Sarah Martinez', time: '2:00 PM', type: 'Portrait' },
                  { client: 'James Wilson', time: '4:30 PM', type: 'Wedding' }
                ].map((booking, i) => (
                  <div key={i} style={{
                    padding: '0.75rem',
                    backgroundColor: '#F8FAFC',
                    borderRadius: '8px',
                    marginBottom: '0.5rem',
                    border: '1px solid #E2E8F0'
                  }}>
                    <div style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1E293B',
                      marginBottom: '0.25rem'
                    }}>
                      {booking.client}
                    </div>
                    <div style={{
                      fontSize: '0.75rem',
                      color: '#64748B',
                      display: 'flex',
                      gap: '1rem'
                    }}>
                      <span>{booking.time}</span>
                      <span>•</span>
                      <span>{booking.type}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section style={{
        padding: '6rem 2rem',
        backgroundColor: '#FFFFFF'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          {/* Section Title */}
          <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
            <h2 style={{
              fontSize: '2.5rem',
              fontWeight: '700',
              color: '#1E293B',
              marginBottom: '1rem'
            }}>
              How It Works
            </h2>
            <p style={{
              fontSize: '1.125rem',
              color: '#475569',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              Book your perfect photographer in four simple steps
            </p>
          </div>

          {/* Steps Wrapper */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '2rem'
          }}>
            {/* Step 1 Card */}
            <div style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              padding: '2.5rem',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              border: '1px solid #E2E8F0',
              position: 'relative',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#2563EB';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#E2E8F0';
            }}
            >
              {/* Step Number */}
              <div style={{
                position: 'absolute',
                top: '2rem',
                right: '2rem',
                fontSize: '3rem',
                fontWeight: '800',
                color: '#E2E8F0',
                lineHeight: 1
              }}>
                01
              </div>
              
              {/* Icon 1 */}
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#DBEAFE',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.5rem'
              }}>
                <Search size={32} color="#2563EB" />
              </div>

              {/* Title */}
              <h3 style={{
                fontSize: '1.5rem',
                fontWeight: '600',
                color: '#1E293B',
                marginBottom: '1rem'
              }}>
                Search & Discover
              </h3>

              {/* Description */}
              <p style={{
                fontSize: '1rem',
                color: '#64748B',
                lineHeight: '1.6'
              }}>
                Browse our curated collection of talented photographers. Filter by location, specialty, price, and ratings to find your perfect match.
              </p>
            </div>

            {/* Step 2 Card */}
            <div style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              padding: '2.5rem',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              border: '1px solid #E2E8F0',
              position: 'relative',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#2563EB';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#E2E8F0';
            }}
            >
              {/* Step Number */}
              <div style={{
                position: 'absolute',
                top: '2rem',
                right: '2rem',
                fontSize: '3rem',
                fontWeight: '800',
                color: '#E2E8F0',
                lineHeight: 1
              }}>
                02
              </div>
              
              {/* Icon 2 */}
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#DBEAFE',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.5rem'
              }}>
                <Camera size={32} color="#2563EB" />
              </div>

              {/* Title */}
              <h3 style={{
                fontSize: '1.5rem',
                fontWeight: '600',
                color: '#1E293B',
                marginBottom: '1rem'
              }}>
                Review Portfolios
              </h3>

              {/* Description */}
              <p style={{
                fontSize: '1rem',
                color: '#64748B',
                lineHeight: '1.6'
              }}>
                Explore stunning portfolios, read reviews from past clients, and see examples of their work to ensure they match your vision.
              </p>
            </div>

            {/* Step 3 Card */}
            <div style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              padding: '2.5rem',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              border: '1px solid #E2E8F0',
              position: 'relative',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#2563EB';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#E2E8F0';
            }}
            >
              {/* Step Number */}
              <div style={{
                position: 'absolute',
                top: '2rem',
                right: '2rem',
                fontSize: '3rem',
                fontWeight: '800',
                color: '#E2E8F0',
                lineHeight: 1
              }}>
                03
              </div>
              
              {/* Icon 3 */}
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#DBEAFE',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.5rem'
              }}>
                <Calendar size={32} color="#2563EB" />
              </div>

              {/* Title */}
              <h3 style={{
                fontSize: '1.5rem',
                fontWeight: '600',
                color: '#1E293B',
                marginBottom: '1rem'
              }}>
                Select Date & Time
              </h3>

              {/* Description */}
              <p style={{
                fontSize: '1rem',
                color: '#64748B',
                lineHeight: '1.6'
              }}>
                Choose your preferred date, time, and session duration. Check real-time availability and select what works best for your schedule.
              </p>
            </div>

            {/* Step 4 Card */}
            <div style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              padding: '2.5rem',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              border: '1px solid #E2E8F0',
              position: 'relative',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#2563EB';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
              e.currentTarget.style.borderColor = '#E2E8F0';
            }}
            >
              {/* Step Number */}
              <div style={{
                position: 'absolute',
                top: '2rem',
                right: '2rem',
                fontSize: '3rem',
                fontWeight: '800',
                color: '#E2E8F0',
                lineHeight: 1
              }}>
                04
              </div>
              
              {/* Icon 4 */}
              <div style={{
                width: '64px',
                height: '64px',
                backgroundColor: '#DBEAFE',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1.5rem'
              }}>
                <CheckCircle size={32} color="#2563EB" />
              </div>

              {/* Title */}
              <h3 style={{
                fontSize: '1.5rem',
                fontWeight: '600',
                color: '#1E293B',
                marginBottom: '1rem'
              }}>
                Book & Confirm
              </h3>

              {/* Description */}
              <p style={{
                fontSize: '1rem',
                color: '#64748B',
                lineHeight: '1.6'
              }}>
                Complete your booking with secure payment and receive instant confirmation. Your photographer will be in touch shortly!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Photographers Section */}
      <section style={{
        padding: '6rem 2rem',
        backgroundColor: '#F8FAFC'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '3rem',
            flexWrap: 'wrap',
            gap: '1rem'
          }}>
            <div>
              <h2 style={{
                fontSize: '2.5rem',
                fontWeight: '700',
                color: '#1E293B',
                marginBottom: '0.5rem'
              }}>
                Featured Photographers
              </h2>
              <p style={{
                fontSize: '1.125rem',
                color: '#475569'
              }}>
                Handpicked professionals with excellent reviews
              </p>
            </div>
            <button
              onClick={() => onNavigate('photographers')}
              style={{
                backgroundColor: 'transparent',
                color: '#2563EB',
                border: '2px solid #2563EB',
                borderRadius: '12px',
                padding: '0.875rem 1.5rem',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#EFF6FF';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              View All
              <ArrowRight size={18} />
            </button>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '2rem'
          }}>
            {[
              {
                name: 'Emma van Bergen',
                specialty: 'Portrait & Wedding',
                rating: 4.9,
                reviews: 127,
                rate: 150,
                image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330'
              },
              {
                name: 'Thomas de Vries',
                specialty: 'Commercial & Product',
                rating: 4.8,
                reviews: 94,
                rate: 120,
                image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d'
              },
              {
                name: 'Sophie Janssen',
                specialty: 'Nature & Landscape',
                rating: 5.0,
                reviews: 73,
                rate: 100,
                image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80'
              }
            ].map((photographer, index) => (
              <div
                key={index}
                onClick={() => onNavigate('photographers')}
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '16px',
                  overflow: 'hidden',
                  boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                }}
              >
                <div style={{
                  position: 'relative',
                  paddingBottom: '75%',
                  backgroundColor: '#F1F5F9'
                }}>
                  <ImageWithFallback
                    src={photographer.image}
                    alt={photographer.name}
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover'
                    }}
                  />
                  <div style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    backgroundColor: '#FFFFFF',
                    borderRadius: '8px',
                    padding: '0.5rem 0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)'
                  }}>
                    <Star size={14} fill="#F59E0B" color="#F59E0B" />
                    <span style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1E293B'
                    }}>
                      {photographer.rating}
                    </span>
                  </div>
                </div>

                <div style={{ padding: '1.5rem' }}>
                  <h3 style={{
                    fontSize: '1.25rem',
                    fontWeight: '600',
                    color: '#1E293B',
                    marginBottom: '0.5rem'
                  }}>
                    {photographer.name}
                  </h3>
                  <p style={{
                    fontSize: '0.875rem',
                    color: '#2563EB',
                    fontWeight: '500',
                    marginBottom: '1rem'
                  }}>
                    {photographer.specialty}
                  </p>

                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    paddingTop: '1rem',
                    borderTop: '1px solid #E2E8F0'
                  }}>
                    <div>
                      <div style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        color: '#1E293B'
                      }}>
                        €{photographer.rate}
                      </div>
                      <div style={{
                        fontSize: '0.75rem',
                        color: '#64748B'
                      }}>
                        per hour
                      </div>
                    </div>
                    <div style={{
                      fontSize: '0.875rem',
                      color: '#64748B'
                    }}>
                      {photographer.reviews} reviews
                    </div>
                  </div>

                  <button
                    style={{
                      width: '100%',
                      marginTop: '1rem',
                      backgroundColor: '#2563EB',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '8px',
                      padding: '0.75rem',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = '#1E40AF';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = '#2563EB';
                    }}
                  >
                    View Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{
        padding: '6rem 2rem',
        backgroundColor: '#2563EB',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          maxWidth: '800px',
          margin: '0 auto',
          textAlign: 'center',
          position: 'relative',
          zIndex: 1
        }}>
          <h2 style={{
            fontSize: '2.5rem',
            fontWeight: '700',
            color: '#FFFFFF',
            marginBottom: '1.5rem'
          }}>
            Ready to Find Your Photographer?
          </h2>
          <p style={{
            fontSize: '1.25rem',
            color: '#DBEAFE',
            marginBottom: '2.5rem',
            lineHeight: '1.6'
          }}>
            Join thousands of satisfied clients and book your perfect photography session today.
          </p>
          <button
            onClick={() => onNavigate('photographers')}
            style={{
              backgroundColor: '#FFFFFF',
              color: '#2563EB',
              border: 'none',
              borderRadius: '12px',
              padding: '1rem 2.5rem',
              fontSize: '1.125rem',
              fontWeight: '600',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.05)';
              e.currentTarget.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            Get Started Now
            <ArrowRight size={20} />
          </button>
        </div>
      </section>
    </div>
  );
}
