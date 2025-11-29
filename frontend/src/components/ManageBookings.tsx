import React, { useState } from 'react';
import { Calendar, Clock, MapPin, User, X, Edit2, CheckCircle, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface Booking {
  id: string;
  photographerId: string;
  photographerName: string;
  photographerImage: string;
  date: string;
  time: string;
  duration: number;
  location: string;
  sessionType: string;
  totalPrice: number;
  status: 'upcoming' | 'past' | 'cancelled';
  bookingDate: string;
}

const mockBookings: Booking[] = [
  {
    id: '1',
    photographerId: '1',
    photographerName: 'Emma van Bergen',
    photographerImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    date: '2024-12-15',
    time: '14:00',
    duration: 2,
    location: 'Amsterdam Central Park',
    sessionType: 'Portrait Session',
    totalPrice: 300,
    status: 'upcoming',
    bookingDate: '2024-11-20'
  },
  {
    id: '2',
    photographerId: '2',
    photographerName: 'Thomas de Vries',
    photographerImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    date: '2024-12-22',
    time: '10:00',
    duration: 4,
    location: 'Rotterdam Studio',
    sessionType: 'Product Photography',
    totalPrice: 480,
    status: 'upcoming',
    bookingDate: '2024-11-18'
  },
  {
    id: '3',
    photographerId: '3',
    photographerName: 'Sophie Janssen',
    photographerImage: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80',
    date: '2024-10-05',
    time: '08:00',
    duration: 3,
    location: 'Utrecht Countryside',
    sessionType: 'Landscape Photography',
    totalPrice: 300,
    status: 'past',
    bookingDate: '2024-09-28'
  },
  {
    id: '4',
    photographerId: '1',
    photographerName: 'Emma van Bergen',
    photographerImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    date: '2024-09-12',
    time: '16:00',
    duration: 3,
    location: 'Amsterdam Wedding Venue',
    sessionType: 'Wedding Photography',
    totalPrice: 450,
    status: 'past',
    bookingDate: '2024-08-15'
  }
];

export default function ManageBookings() {
  const [view, setView] = useState<'list' | 'calendar'>('list');
  const [filter, setFilter] = useState<'all' | 'upcoming' | 'past'>('upcoming');
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [currentMonth, setCurrentMonth] = useState(new Date());

  const filteredBookings = mockBookings.filter(booking => {
    if (filter === 'all') return true;
    return booking.status === filter;
  });

  const handleCancelBooking = (bookingId: string) => {
    // In real app, send cancellation to Supabase
    console.log('Cancelling booking:', bookingId);
    alert('Booking cancelled successfully. Refund will be processed within 5-7 business days.');
    setShowCancelModal(false);
    setSelectedBooking(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'upcoming':
        return '#10B981';
      case 'past':
        return '#64748B';
      case 'cancelled':
        return '#EF4444';
      default:
        return '#64748B';
    }
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();
    
    return { daysInMonth, startingDayOfWeek, year, month };
  };

  const getBookingsForDate = (date: Date) => {
    const dateString = date.toISOString().split('T')[0];
    return filteredBookings.filter(booking => booking.date === dateString);
  };

  const renderCalendarView = () => {
    const { daysInMonth, startingDayOfWeek, year, month } = getDaysInMonth(currentMonth);
    const days = [];
    const monthName = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(<div key={`empty-${i}`} style={{ padding: '1rem' }} />);
    }

    // Add cells for each day of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const bookingsForDay = getBookingsForDate(date);
      const isToday = new Date().toDateString() === date.toDateString();

      days.push(
        <div
          key={day}
          style={{
            padding: '0.75rem',
            border: '1px solid #E2E8F0',
            minHeight: '100px',
            backgroundColor: isToday ? '#DBEAFE' : '#FFFFFF',
            position: 'relative'
          }}
        >
          <div style={{
            fontWeight: isToday ? '700' : '600',
            color: isToday ? '#1E3A8A' : '#1E293B',
            marginBottom: '0.5rem'
          }}>
            {day}
          </div>
          {bookingsForDay.map(booking => (
            <div
              key={booking.id}
              onClick={() => setSelectedBooking(booking)}
              style={{
                padding: '0.25rem 0.5rem',
                backgroundColor: booking.status === 'upcoming' ? '#10B981' : '#64748B',
                color: '#FFFFFF',
                borderRadius: '4px',
                fontSize: '0.75rem',
                marginBottom: '0.25rem',
                cursor: 'pointer',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}
            >
              {booking.time} - {booking.photographerName}
            </div>
          ))}
        </div>
      );
    }

    return (
      <div>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '1.5rem',
          padding: '1rem',
          backgroundColor: '#F1F5F9',
          borderRadius: '12px'
        }}>
          <button
            onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              color: '#1E3A8A'
            }}
          >
            <ChevronLeft size={24} />
          </button>
          <h3 style={{
            fontSize: '1.5rem',
            fontWeight: '700',
            color: '#1E293B'
          }}>
            {monthName}
          </h3>
          <button
            onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              color: '#1E3A8A'
            }}
          >
            <ChevronRight size={24} />
          </button>
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(7, 1fr)',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          overflow: 'hidden',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
        }}>
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div
              key={day}
              style={{
                padding: '1rem',
                fontWeight: '700',
                textAlign: 'center',
                backgroundColor: '#F1F5F9',
                borderBottom: '2px solid #E2E8F0',
                color: '#1E293B'
              }}
            >
              {day}
            </div>
          ))}
          {days}
        </div>
      </div>
    );
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#F1F5F9', padding: '3rem 2rem' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '3rem' }}>
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: '700',
            color: '#1E293B',
            marginBottom: '0.5rem'
          }}>
            Manage My Bookings
          </h1>
          <p style={{
            fontSize: '1.125rem',
            color: '#475569'
          }}>
            View and manage all your photography session bookings
          </p>
        </div>

        {/* View Toggle & Filters */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            padding: '0.25rem',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
          }}>
            <button
              onClick={() => setView('list')}
              style={{
                padding: '0.625rem 1.25rem',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: view === 'list' ? '#1E3A8A' : 'transparent',
                color: view === 'list' ? '#FFFFFF' : '#64748B',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              List View
            </button>
            <button
              onClick={() => setView('calendar')}
              style={{
                padding: '0.625rem 1.25rem',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: view === 'calendar' ? '#1E3A8A' : 'transparent',
                color: view === 'calendar' ? '#FFFFFF' : '#64748B',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              Calendar View
            </button>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {['all', 'upcoming', 'past'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f as any)}
                style={{
                  padding: '0.625rem 1.25rem',
                  borderRadius: '8px',
                  border: filter === f ? '2px solid #1E3A8A' : '2px solid #E2E8F0',
                  backgroundColor: filter === f ? '#DBEAFE' : '#FFFFFF',
                  color: filter === f ? '#1E3A8A' : '#64748B',
                  fontWeight: '600',
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  transition: 'all 0.2s ease'
                }}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {view === 'calendar' ? renderCalendarView() : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {filteredBookings.length === 0 ? (
              <div style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '16px',
                padding: '4rem 2rem',
                textAlign: 'center',
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
              }}>
                <AlertCircle size={48} color="#94A3B8" style={{ margin: '0 auto 1rem' }} />
                <h3 style={{
                  fontSize: '1.5rem',
                  fontWeight: '600',
                  color: '#1E293B',
                  marginBottom: '0.5rem'
                }}>
                  No bookings found
                </h3>
                <p style={{ color: '#64748B' }}>
                  You don't have any {filter !== 'all' ? filter : ''} bookings yet.
                </p>
              </div>
            ) : (
              filteredBookings.map(booking => (
                <div
                  key={booking.id}
                  style={{
                    backgroundColor: '#FFFFFF',
                    borderRadius: '16px',
                    padding: '2rem',
                    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                    display: 'grid',
                    gridTemplateColumns: 'auto 1fr auto',
                    gap: '2rem',
                    alignItems: 'center',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                  }}
                >
                  {/* Photographer Image */}
                  <ImageWithFallback
                    src={booking.photographerImage}
                    alt={booking.photographerName}
                    style={{
                      width: '80px',
                      height: '80px',
                      borderRadius: '12px',
                      objectFit: 'cover'
                    }}
                  />

                  {/* Booking Details */}
                  <div>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '1rem',
                      marginBottom: '0.75rem'
                    }}>
                      <h3 style={{
                        fontSize: '1.25rem',
                        fontWeight: '600',
                        color: '#1E293B'
                      }}>
                        {booking.photographerName}
                      </h3>
                      <span style={{
                        padding: '0.25rem 0.75rem',
                        borderRadius: '6px',
                        fontSize: '0.75rem',
                        fontWeight: '600',
                        backgroundColor: booking.status === 'upcoming' ? '#D1FAE5' : '#F1F5F9',
                        color: getStatusColor(booking.status),
                        textTransform: 'uppercase'
                      }}>
                        {booking.status}
                      </span>
                    </div>

                    <div style={{
                      fontSize: '0.875rem',
                      color: '#2563EB',
                      fontWeight: '600',
                      marginBottom: '1rem'
                    }}>
                      {booking.sessionType}
                    </div>

                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                      gap: '1rem',
                      color: '#64748B',
                      fontSize: '0.875rem'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Calendar size={16} />
                        <span>{formatDate(booking.date)}</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Clock size={16} />
                        <span>{booking.time} ({booking.duration} hours)</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <MapPin size={16} />
                        <span>{booking.location}</span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'flex-end',
                    gap: '1rem'
                  }}>
                    <div style={{
                      fontSize: '1.75rem',
                      fontWeight: '700',
                      color: '#1E3A8A'
                    }}>
                      €{booking.totalPrice}
                    </div>

                    {booking.status === 'upcoming' && (
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button
                          onClick={() => setSelectedBooking(booking)}
                          style={{
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            border: '2px solid #1E3A8A',
                            backgroundColor: 'transparent',
                            color: '#1E3A8A',
                            fontWeight: '600',
                            cursor: 'pointer',
                            fontSize: '0.875rem',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            transition: 'all 0.2s ease'
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.backgroundColor = '#DBEAFE';
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.backgroundColor = 'transparent';
                          }}
                        >
                          <Edit2 size={14} />
                          Reschedule
                        </button>
                        <button
                          onClick={() => {
                            setSelectedBooking(booking);
                            setShowCancelModal(true);
                          }}
                          style={{
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            border: '2px solid #EF4444',
                            backgroundColor: 'transparent',
                            color: '#EF4444',
                            fontWeight: '600',
                            cursor: 'pointer',
                            fontSize: '0.875rem',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            transition: 'all 0.2s ease'
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.backgroundColor = '#FEE2E2';
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.backgroundColor = 'transparent';
                          }}
                        >
                          <X size={14} />
                          Cancel
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* Cancel Confirmation Modal */}
      {showCancelModal && selectedBooking && (
        <div
          onClick={() => setShowCancelModal(false)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '2rem'
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              padding: '2rem',
              maxWidth: '500px',
              width: '100%',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)'
            }}
          >
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '1.5rem'
            }}>
              <h3 style={{
                fontSize: '1.5rem',
                fontWeight: '700',
                color: '#1E293B'
              }}>
                Cancel Booking?
              </h3>
              <button
                onClick={() => setShowCancelModal(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '0.5rem',
                  color: '#64748B'
                }}
              >
                <X size={24} />
              </button>
            </div>

            <p style={{
              color: '#475569',
              marginBottom: '1.5rem',
              lineHeight: '1.6'
            }}>
              Are you sure you want to cancel your booking with <strong>{selectedBooking.photographerName}</strong> on {formatDate(selectedBooking.date)}?
              This action cannot be undone, but you will receive a full refund within 5-7 business days.
            </p>

            <div style={{
              display: 'flex',
              gap: '1rem',
              justifyContent: 'flex-end'
            }}>
              <button
                onClick={() => setShowCancelModal(false)}
                style={{
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px',
                  border: '2px solid #E2E8F0',
                  backgroundColor: '#FFFFFF',
                  color: '#64748B',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#F1F5F9';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#FFFFFF';
                }}
              >
                Keep Booking
              </button>
              <button
                onClick={() => handleCancelBooking(selectedBooking.id)}
                style={{
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: '#EF4444',
                  color: '#FFFFFF',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#DC2626';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#EF4444';
                }}
              >
                Yes, Cancel Booking
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
