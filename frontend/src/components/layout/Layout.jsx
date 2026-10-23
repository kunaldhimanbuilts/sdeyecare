import Header from "./Header";

function Layout({ children }) {
  return (
   
    <div className="flex bg-gray-100 ">

      <div className="flex-1">
        
        <div className="no-print">
          <Header />
        </div>
        
        <div className=" overflow-x-hidden max-w-full">{children}</div>
      </div>
    </div>
  );
}

export default Layout;