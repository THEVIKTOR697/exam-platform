"use client";

import { usePathname } from "next/navigation";
import Navbar from "@/components/ui/navbar";

export default function ClientLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();
    const hideNavbar = pathname === "/login";

    return (
        <>
            {!hideNavbar && <Navbar />}
            {children}
        </>
    );
}
