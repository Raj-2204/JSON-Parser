
const Layout = ({ children }) => {
  return (
    <div className="layout">
      <header className="layout-header">
        <h1>JSON Parser & Validator</h1>
        <p>Advanced JSON parsing with semantic validation and parse tree visualization</p>
      </header>
      
      <main className="layout-main">
        {children}
      </main>
      
      <footer className="layout-footer">
        <p>Built with React + Vite | Backend powered by Python Flask</p>
      </footer>
    </div>
  );
};

export default Layout;