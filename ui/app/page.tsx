export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center h-screen bg-neutral-50 text-neutral-950">

            <img src="/img/Full-logo.png" alt="Full Logo"/>

            <a href="/login" className="px-8 py-3 rounded-lg bg-neutral-950 text-white font-medium hover:shadow-lg hover:scale-105 transform transition duration-300">
                Get Started
            </a>
        
        </div>
    );
}