
const Layout = ({ children }) => {
  return (
    <div className="layout">
      <header className="layout-header">
        <h1>JSON Parser & Validator</h1>
        <p>Advanced JSON parsing</p>
      </header>
      
      <main className="layout-main">
        {children}
      </main>
      
      <footer className="layout-footer">
        <p>&copy Rajveer Singh</p>
      </footer>
    </div>
  );
};

export default Layout;