#include "client.h"

#include <cstdlib>
#include <iostream>
#include <boost/bind.hpp>
#include <boost/asio.hpp>
#include <boost/asio/ssl.hpp>
#include <boost/asio/ssl/context.hpp>


int main(int argc, char* argv[])
{
  try
  {
//    if (argc != 3)
//    {
//      std::cerr << "Usage: client <host> <port>\n";
//      return 1;
//    }

    boost::asio::io_service io_service;

    boost::asio::ip::tcp::resolver resolver(io_service);
    boost::asio::ip::tcp::resolver::query query("37.9.171.172", "4115");
//    boost::asio::ip::tcp::resolver::query query(argv[1], argv[2]);
    boost::asio::ip::tcp::resolver::iterator iterator = resolver.resolve(query);

    boost::asio::ssl::context ctx(boost::asio::ssl::context::tlsv12);
    ctx.use_rsa_private_key_file("../keyfile", boost::asio::ssl::context::pem);
    ctx.use_certificate_chain_file("../certfile");

    ATPClient c(io_service, ctx, iterator);

    io_service.run();
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}
