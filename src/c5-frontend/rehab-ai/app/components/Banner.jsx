import './Banner.css';

// Banner component
const Banner = ({ title, subtitle, buttonText, buttonUrl, imageUrl }) => (
    <div className="bannerContainer">
        <img src={imageUrl} alt="hero-banner" />
        <div className="overlayContent">
            <h1>{title}</h1>
            <h3>{subtitle}</h3>
        </div>
    </div>
    
);

export default Banner;
