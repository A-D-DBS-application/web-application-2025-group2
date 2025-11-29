import React, { useState } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { HomePage } from './components/HomePage';
import { LoginPage } from './components/LoginPage';
import { RegisterPage } from './components/RegisterPage';
import PhotographersDirectory from './components/PhotographersDirectory';
import PhotographerProfile from './components/PhotographerProfile';
import PhotographerDashboard from './components/PhotographerDashboard';
import ManageBookings from './components/ManageBookings';
import BookingModal, { BookingFormData } from './components/BookingModal';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedPhotographerId, setSelectedPhotographerId] = useState<string | null>(null);
  const [bookingPhotographer, setBookingPhotographer] = useState<{ id: string; name: string; rate: number } | null>(null);

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
    setSelectedPhotographerId(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleViewProfile = (photographerId: string) => {
    setSelectedPhotographerId(photographerId);
  };

  const handleBackToDirectory = () => {
    setSelectedPhotographerId(null);
  };

  const handleBookSession = (photographerId: string) => {
    // In real app, fetch photographer details
    setBookingPhotographer({
      id: photographerId,
      name: 'Emma van Bergen',
      rate: 150
    });
  };

  const handleBookingSubmit = (bookingData: BookingFormData) => {
    // In real app, send to Supabase
    console.log('Booking submitted:', bookingData);
    alert('Booking request submitted successfully! The photographer will contact you soon.');
    setBookingPhotographer(null);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />;
      case 'login':
        return <LoginPage onNavigate={handleNavigate} />;
      case 'register':
        return <RegisterPage onNavigate={handleNavigate} />;
      case 'photographers':
        if (selectedPhotographerId) {
          return (
            <PhotographerProfile
              photographerId={selectedPhotographerId}
              onBack={handleBackToDirectory}
              onBookSession={handleBookSession}
            />
          );
        }
        return <PhotographersDirectory onViewProfile={handleViewProfile} />;
      case 'dashboard':
        return <PhotographerDashboard />;
      case 'bookings':
        return <ManageBookings />;
      case 'about':
        return <HomePage onNavigate={handleNavigate} />;
      default:
        return <HomePage onNavigate={handleNavigate} />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header currentPage={currentPage} onNavigate={handleNavigate} />
      <main className="flex-1">
        {renderPage()}
      </main>
      <Footer />
      
      {/* Booking Modal */}
      {bookingPhotographer && (
        <BookingModal
          photographerId={bookingPhotographer.id}
          photographerName={bookingPhotographer.name}
          hourlyRate={bookingPhotographer.rate}
          onClose={() => setBookingPhotographer(null)}
          onSubmit={handleBookingSubmit}
        />
      )}
    </div>
  );
}

export default App;